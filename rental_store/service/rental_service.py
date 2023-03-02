import uuid
from datetime import date

from rental_store.models import FilmRentRequestModel, FilmRentResponseModel, Film, FilmReturnRequest, ReturnFilmResponse
from rental_store.repository.data_storage import InMemoryFilmRepository, FilmRentalDetails, InMemoryRentalsRepository, \
    Rental
from rental_store.service.calculator import calculate_rent_charge

film_repository = InMemoryFilmRepository()
rental_repository = InMemoryRentalsRepository()


class RentalService:

    # assumptions:
    # 1. we allow partial rentals in case some movies are not available
    # 2. for now we assume we have only 1 Rental per customer
    @staticmethod
    def rent(request: FilmRentRequestModel) -> FilmRentResponseModel:
        not_available_films: set[Film] = set()
        available_films: set[Film] = set()

        for film_to_be_rented in request.rented_films:
            film = film_repository.films.get(film_to_be_rented.film_id)
            if film.available_items > 0:
                charge, currency = calculate_rent_charge(price_list, film,
                                                         film_to_be_rented.up_front_days)  # TODO: remove currency

                film_rental_detail = FilmRentalDetails(film_id=film_to_be_rented.film_id,
                                                       rental_date=date.date.today(),
                                                       charged=charge,
                                                       up_front_days=film_to_be_rented.up_front_days)
                available_films.add(film_rental_detail)
            else:
                not_available_films.add(film_to_be_rented.film_id)

        for film in available_films:
            film_repository.mark_as_rented(film.id)

        rental_repository.save(Rental(uuid.uuid4(), request.customer_id, available_films))

        return available_films


    # assumptions:
    # 1. they must pay upon the return
    # 2. they might return only a subset of already rented movies
    # 3. for the movies not returned they will pay surcharge when they return it
    # 4. if they return movie earlier they will not get any money back
    @staticmethod
    def return(request: FilmReturnRequest) -> ReturnFilmResponse:
        rental = rental_repository.find_by_customer_id(request.customer_id)

        for returned_film in request.returned_films:
            details = rental.details.pop(returned_film)
            # if surcharge is needed:
            #  film_repo.get film
            # calculate_rent_surcharge(price_list, details.)


            film_repository.mark_as_returned(returned_film)

        if len(rental.details) <= 0:
            rental_repository.delete(rental)
        else:
            rental_repository.save(rental)

        return ReturnFilmResponse()





